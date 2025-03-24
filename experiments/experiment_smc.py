from experiment import (
    replace_and_run,
    arg_parser
)

def main():
    parser = arg_parser()
    parser.add_argument(
        '-t', '--time', type=int,
        help='The maximum simulation time of the SMC queries.'
    )
    parser.add_argument(
        '-s', '--simulations', type=int,
        help='The number of simulations to perform in each SMC query.'
    )

    args = parser.parse_args()

    replace_and_run(
        args.model, args.query,
        args.output, args.query_output, args.log_output,
        {
            '<<T>>': str(args.time),
            '<<N>>': str(args.simulations)
        }
    )

if __name__ == "__main__":
    main()