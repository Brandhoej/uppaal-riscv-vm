from experiment import (
    replace_and_run,
    arg_parser
)

def main():
    parser = arg_parser()
    args = parser.parse_args()

    replace_and_run(
        args.model, args.query,
        args.query_output, args.log_output,
        { },
    )

if __name__ == "__main__":
    main()