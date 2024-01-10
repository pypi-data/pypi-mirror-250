from logging import getLogger

logger = getLogger(__file__)


class PrintLogger:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self.formated_prefix = f"{prefix}:\t"
        self.output_buffer = open("logs.json", "w+")
        self.output_buffer.write("")
        self.output_buffer.flush()
        logger.debug(
            f"Creating logger for {prefix} with buffer {self.output_buffer.name}"
        )

    def __call__(self, *args, **kwargs):
        new_args = [
            str(a).replace("\n", f"\n{self.formated_prefix}") for a in args
        ]
        print(self.formated_prefix, *new_args, **kwargs)
        logs = self.formated_prefix + str(args[0])
        self.output_buffer.write(logs)
        self.output_buffer.write("\n")
        self.output_buffer.flush()

    def get_logged_data(self):
        self.output_buffer.seek(0)
        return self.output_buffer.read()
