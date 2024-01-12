from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

access_token = "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"

checkpoint = "bigcode/starcoder"

tokenizer = AutoTokenizer.from_pretrained(
    checkpoint, padding_side="left", token=access_token
)
model = AutoModelForCausalLM.from_pretrained(
    checkpoint,
    token=access_token,
    load_in_8bit=True,
    device_map="auto",
)
tokenizer.pad_token_id = tokenizer.eos_token_id

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)


def get_schema(db_dir: str, db_id: str) -> str:
    import glob

    schema_files = glob.glob(f"{db_dir}/{db_id}/*.sql")
    if len(schema_files) == 0:
        print(f"Schema file not found for {db_dir}/{db_id}")
        return None
    if len(schema_files) > 1:
        print(f"Multiple schema files found for {db_dir}/{db_id}")
        return None

    try:
        with open(schema_files[0]) as f:
            # Extract all the "CREATE TABLE (...);" statements
            schema = ""
            in_create_table = False
            for line in f:
                line = line.strip()
                if "CREATE TABLE " in line.upper():
                    in_create_table = True
                if in_create_table:
                    schema += line + "\n"
                if ");" in line:
                    in_create_table = False
            schema = schema.replace("`", '"')
    except Exception as e:
        print(e)
        return None

    return schema


def get_prompt(spider_path: str, db_id: str, question: str) -> str:
    schema = get_schema(f"{spider_path}/database", db_id)
    if schema is None:
        schema = ""

    prompt = f"""{schema}

Translate the following question into SQL.

Question: {question}
SQL: """
    return prompt


def get_query(prompt: str, output: dict) -> str:
    try:
        generated = output["generated_text"][len(prompt) :].strip()
        query = " ".join(
            generated[: generated.index(";") + 1].split()
        )  # TODO: some ends with '''
    except Exception as e:
        print("get_query error:", e)
        print(f"{generated=}")
        return ""
    return query


def run_sqlite(spider_path: str, db_id: str, query: str):
    import subprocess

    db_path = f"{spider_path}/database/{db_id}/{db_id}.sqlite"
    cmd = ["sqlite3", db_path, query]
    return subprocess.run(cmd, capture_output=True, encoding="utf-8")


def run_spider(spider_path: str, split: str):
    import json
    import os

    assert split in ("train_spider", "train_others", "dev")
    with open(os.path.join(spider_path, f"{split}.json")) as f:
        dataset = json.load(f)
    print(f"{len(dataset)=}")

    # no schema.sql
    skipping = [
        db_id
        for db_id in os.listdir(os.path.join(spider_path, "database"))
        if not os.path.isfile(
            os.path.join(spider_path, "database", db_id, "schema.sql")
        )
    ]
    # print(skipping)
    dataset = [data for data in dataset if data["db_id"] not in skipping]
    print(f"{len(dataset)=}")

    prompts = [
        get_prompt(spider_path, data["db_id"], data["question"]) for data in dataset
    ]
    print("get_prompt done. generating ...")
    generated_texts = generator(
        prompts,
        max_new_tokens=256,
        pad_token_id=tokenizer.eos_token_id,
        batch_size=16,
    )
    print("generaation done.")
    assert len(generated_texts) == len(dataset)

    idx_error = []
    for i, data in enumerate(dataset):
        db_id = data["db_id"]

        gold_query = data["query"]
        gold_result = run_sqlite(spider_path, db_id, gold_query)

        query = get_query(prompts[i], generated_texts[i][0])
        result = run_sqlite(spider_path, db_id, query)

        if result.stdout.strip() != gold_result.stdout.strip():
            idx_error.append(i)

            print("=" * 10)
            print(i, db_id)
            print(data["question"])
            print(gold_query)
            print(gold_result.stdout)
            print("-" * 5)
            print(query)
            print(result.stdout)
            print(result.stderr)
            print("=" * 10)

    accuracy = 1 - len(idx_error) / len(dataset)
    print(f"{accuracy=}")
    print(idx_error)


run_spider("../data/spider", "train_spider")
