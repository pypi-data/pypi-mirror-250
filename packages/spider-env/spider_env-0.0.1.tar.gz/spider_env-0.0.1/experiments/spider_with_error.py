from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

access_token = "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"

checkpoint = "bigcode/starcoder"
device = "cuda"

tokenizer = AutoTokenizer.from_pretrained(
    checkpoint, padding_side="left", token=access_token
)
model = AutoModelForCausalLM.from_pretrained(checkpoint, token=access_token).to(device)
tokenizer.pad_token_id = tokenizer.eos_token_id

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=device,
)


# TODO: some schema is different
def get_prompt(spider_path: str, db_id: str, question: str) -> str:
    schema_path = f"{spider_path}/database/{db_id}/schema.sql"
    with open(schema_path) as f:
        lines = [
            line.strip()
            for line in f
            if line.startswith("CREATE TABLE")
            or line.startswith('"')
            or line.startswith(");")
        ]

    schema = "\n".join(lines)

    prompt = f"""{schema}

Translate the following question into SQL.

Question: {question}
SQL: """
    return prompt


def get_prompt_with_errors(
    spider_path: str, db_id: str, question: str, query: str, error: str
) -> str:
    schema_path = f"{spider_path}/database/{db_id}/schema.sql"
    with open(schema_path) as f:
        lines = [
            line.strip()
            for line in f
            if line.startswith("CREATE TABLE")
            or line.startswith('"')
            or line.startswith(");")
        ]

    schema = "\n".join(lines)

    prompt = f"""{schema}

Translate the following question into SQL.

Question: {question}

SQL: {query}

Feedback: {"The SQL query execution result is wrong" if len(error) == 0 else "The SQL query fails to execute with this error: " + error}

Please fix the SQL.

SQL: """
    return prompt


def get_query(prompt: str, output: dict) -> str:
    try:
        generated = output["generated_text"][len(prompt) :].strip()
        query = " ".join(
            generated[: generated.index(";")].split()
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
    return subprocess.run(cmd, capture_output=True, text=True)


def run_spider(spider_path: str, split: str, previous_error_idx: list):
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

    # Only generate for previous errors.
    dataset = [dataset[i] for i in previous_error_idx]
    print(f"{len(dataset)=}")

    prompts = [
        get_prompt(spider_path, data["db_id"], data["question"]) for data in dataset
    ]
    # TODO: Save the generated queries instead.
    generated_texts = generator(
        prompts,
        max_new_tokens=256,
        pad_token_id=tokenizer.eos_token_id,
        batch_size=32,
    )
    assert len(generated_texts) == len(dataset)
    print("generation done")

    generated_queries = []
    error_messages = []
    for i, data in enumerate(dataset):
        db_id = data["db_id"]

        gold_query = data["query"]
        gold_result = run_sqlite(spider_path, db_id, gold_query)

        query = get_query(prompts[i], generated_texts[i][0])
        result = run_sqlite(spider_path, db_id, query)

        assert result.stdout.strip() != gold_result.stdout.strip()
        generated_queries.append(query)
        error_messages.append(result.stderr.strip())
    assert len(generated_queries) == len(dataset)
    assert len(error_messages) == len(dataset)
    print("error message done")

    prompts_with_errors = [
        get_prompt_with_errors(
            spider_path,
            dataset[i]["db_id"],
            dataset[i]["question"],
            generated_queries[i],
            error_messages[i],
        )
        for i in range(len(error_messages))
    ]
    generated_texts = generator(
        prompts_with_errors,
        max_new_tokens=256,
        pad_token_id=tokenizer.eos_token_id,
        batch_size=16,
    )
    assert len(generated_texts) == len(dataset)
    print("generation with error message done")

    idx_error = []
    for i, data in enumerate(dataset):
        db_id = data["db_id"]

        gold_query = data["query"]
        gold_result = run_sqlite(spider_path, db_id, gold_query)

        query = get_query(prompts_with_errors[i], generated_texts[i][0])
        result = run_sqlite(spider_path, db_id, query)

        if result.stdout.strip() != gold_result.stdout.strip():
            idx_error.append(i)

            print("=" * 10)
            print(i, db_id)
            print(data["question"])
            print(gold_query)
            print(gold_result.stdout)
            print("-" * 5)
            # print(prompts_with_errors[i])
            # print(generated_texts[i][0])
            print(query)
            print(result.stdout)
            print(result.stderr)
            print("=" * 10)

    accuracy = 1 - len(idx_error) / len(dataset)
    print(f"{accuracy=}")
    print(idx_error)


with open("spider.log") as f:
    for line in f:
        pass
    last_line = line
previous_error_idx = eval(last_line)
print(len(previous_error_idx))

run_spider("./data/spider", "train_spider", previous_error_idx)
