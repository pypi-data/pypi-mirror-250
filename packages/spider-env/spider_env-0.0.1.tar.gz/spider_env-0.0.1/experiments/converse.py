class Agent:
    def __init__(self, checkpoint: str, callback=None):
        self.generator = self._get_text_generator(checkpoint)
        self._callback = callback

    # TODO: Add more customization configs: peft, access_token, ddp.
    def _get_text_generator(self, checkpoint: str):
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

        self._tokenizer = AutoTokenizer.from_pretrained(checkpoint, padding_side="left")
        self._tokenizer.pad_token_id = self._tokenizer.eos_token_id

        self._model = AutoModelForCausalLM.from_pretrained(
            checkpoint,
            # load_in_8bit=True,
            device_map="auto",
        )

        self._generator = pipeline(
            "text-generation",
            model=self._model,
            tokenizer=self._tokenizer,
        )

    def generate(self, prompt: str, *args, **kwargs):
        # TODO: Expose configs.
        response = self._generator(
            prompt,
            do_sample=True,
            top_p=0.9,
            num_return_sequences=1,
            max_new_tokens=64,
            pad_token_id=self._tokenizer.eos_token_id,
            batch_size=32,
        )
        assert len(response) == 1
        generated = response[0]["generated_text"]

        if self._callback is None:
            return generated
        else:
            return self._callback(generated, *args, **kwargs)

    def get_message(self, history: list) -> str:
        # Implement for specific task.
        pass


class ActorCriticConversation:
    def __init__(self, actor: Agent, critic: Agent, history=None):
        self._actor, self._critic = actor, critic
        assert len(history) > 0
        self._history = history

    def rollout(self, start: int, max_step: int) -> None:
        self._history = self._history[: start + 1]
        current_step = len(self._history)

        while current_step <= max_step:
            if current_step % 2 == 1:
                message = self._actor.get_message(self._history)
            else:
                message = self._critic.get_message(self._history)

            self._history.append(message)
            current_step += 1
            # TODO: Break on success.

    def get_history(self, step: int = None) -> str:
        if step is None:
            return self._history
        else:
            return self._history[step]

    def reset_history(self, history):
        self._history = history

    def get_reward(self) -> float:
        # TODO: Get reward based on history.
        return 1.0


def run_algo(conversation: ActorCriticConversation, horizon: int, max_rollouts: int):
    for n in range(horizon):
        print(f"{n=}")

        rollouts = []
        for _ in range(max_rollouts):
            conversation.rollout(start=n, max_step=horizon)

            candidate = conversation.get_history(n + 1)
            reward = conversation.get_reward()
            rollouts.append([candidate, reward])

            # DPO stuff
        print(f"{rollouts=}")

        chosen_candidate = rollouts[0][0]  # pick_one
        conversation.reset_history(
            conversation.get_history()[: n + 1] + [chosen_candidate]
        )
        print("history:", conversation.get_history())


# Implement the following for a specific task.


class SqlAgent(Agent):
    def __init__(self, checkpoint: str):
        super().__init__(checkpoint)
        self._spider_path = "./data/spider/"

    def _get_prompt(self, db_id: str, question: str) -> str:
        schema_path = f"{self._spider_path}/database/{db_id}/schema.sql"
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

    def _get_prompt_with_errors(
        self, db_id: str, question: str, query: str, error: str
    ) -> str:
        schema_path = f"{self._spider_path}/database/{db_id}/schema.sql"
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

    def _get_query(self, prompt: str, generated: str) -> str:
        try:
            generated = generated[len(prompt) :].strip()
            query = " ".join(
                generated[: generated.index("\n")].split()
            )  # TODO: some ends with '''
        except Exception as e:
            print("get_query error:", e)
            print(f"{generated=}")
            return ""
        return query

    def get_message(self, history: list) -> str:
        assert len(history) > 0
        db_id, question = history[0].split(":")

        if len(history) == 1:
            prompt = self._get_prompt(db_id, question)
        else:
            assert len(history) > 2
            query = history[-2]
            error = history[-1]
            prompt = self._get_prompt_with_errors(db_id, question, query, error)

        generated = self.generate(prompt)
        query = self._get_query(prompt, generated)

        return query


class ExeAgent(Agent):
    def __init__(self, checkpoint: str):
        super().__init__(checkpoint)
        self._spider_path = "./data/spider/"

    def run_sqlite(self, db_id: str, query: str):
        import subprocess

        db_path = f"{self._spider_path}/database/{db_id}/{db_id}.sqlite"
        cmd = ["sqlite3", db_path, query]
        return subprocess.run(cmd, capture_output=True, encoding="utf-8")

    def get_message(self, history: list) -> str:
        assert len(history) > 1
        db_id, _ = history[0].split(":")
        query = history[-1]

        result = self.run_sqlite(db_id, query)
        error = result.stderr.strip()

        return error


def run_spider():
    actor = SqlAgent(checkpoint="bigcode/starcoder")
    critic = ExeAgent(checkpoint="gpt2")

    example = {
        "db_id": "department_management",
        "question": "How many heads of the departments are older than 56 ?",
    }

    conversation_so_far = [example["db_id"] + ":" + example["question"]]

    conversation = ActorCriticConversation(actor, critic, history=conversation_so_far)
    run_algo(conversation=conversation, horizon=3, max_rollouts=1)


if __name__ == "__main__":
    run_spider()
