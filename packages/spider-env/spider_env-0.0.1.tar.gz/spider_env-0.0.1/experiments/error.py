import sys

assert len(sys.argv) == 2
spider_log_file = sys.argv[1]

all_err_msgs = []
parser_errs = []
semantic_errs = []

with open(spider_log_file) as f:
    for line in f:
        if (("error" in line) or ("Error" in line)) and (
            ("system error" not in line) and ("Super Terrorizer" not in line)
        ):
            all_err_msgs.append(line.strip())

            if (
                ('Error: near """"' in line)
                or ("Error: near \"'''" in line)
                or ("Error: unrecognized token" in line)
                or ("get_query error" in line)
            ):
                parser_errs.append(line)

            if (
                ("ambiguous column name" in line)
                or ("misuse of aggregate" in line)  # syntax error?
                or ("no such column" in line)
                or ("no such table" in line)
            ):
                semantic_errs.append(line)

all_incorrect = eval(line)
print(f"{len(all_incorrect)=}")

print(f"{len(all_err_msgs)=}")
print(f"{len(parser_errs)=}")
print(f"{len(semantic_errs)=}")
for err_msg in [
    "ambiguous column name",
    "misuse of aggregate",
    "no such column",
    "no such table",
]:
    print(err_msg, len([x for x in semantic_errs if err_msg in x]))

all_err_msgs = sorted(all_err_msgs)
print("\n".join(all_err_msgs))
