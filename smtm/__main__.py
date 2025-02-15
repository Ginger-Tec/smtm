"""smtm 모듈의 시작
mode:
    0: simulator with interative mode
    1: execute single simulation
    2: controller for real trading
    3: telegram chatbot controller
    4: mass simulation with config file
    5: make config file for mass simulation

Example) python -m smtm --mode 0
Example) python -m smtm --mode 1
Example) python -m smtm --budget 500 --from_dash_to 201220.170000-201221 --term 1 --strategy 0 --currency BTC
Example) python -m smtm --mode 2 --budget 50000 --term 60 --strategy 0 --currency ETH
Example) python -m smtm --mode 3
Example) python -m smtm --mode 4 --config /data/sma0_simulation.json
Example) python -m smtm --mode 5 --budget 50000 --title SMA_2H_week --strategy 1 --currency ETH --from_dash_to 210804.000000-210811.000000 --offset 120
"""
import argparse
from argparse import RawTextHelpFormatter
import sys
from . import Simulator, Controller, TelegramController, MassSimulator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""자동 거래 시스템 smtm

mode:
    0: simulator with interative mode
    1: execute single simulation
    2: controller for real trading
    3: telegram chatbot controller
    4: mass simulation with config file
    5: make config file for mass simulation

Example) python -m smtm --mode 0
Example) python -m smtm --mode 1
Example) python -m smtm --budget 500 --from_dash_to 201220.170000-201221 --term 1 --strategy 0 --currency BTC
Example) python -m smtm --mode 2 --budget 50000 --term 60 --strategy 0 --currency ETH
Example) python -m smtm --mode 3
Example) python -m smtm --mode 4 --config /data/sma0_simulation.json
Example) python -m smtm --mode 5 --budget 50000 --title SMA_2H_week --strategy 1 --currency ETH --from_dash_to 210804.000000-210811.000000 --offset 120
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("--budget", help="budget", type=int, default=10000)
    parser.add_argument("--term", help="trading tick interval (seconds)", type=int, default="60")
    parser.add_argument("--strategy", help="strategy 0: buy and hold, 1: sma0", default="0")
    parser.add_argument("--trader", help="trader 0: Upbit, 1: Bithumb", default="0")
    parser.add_argument("--currency", help="trading currency e.g.BTC", default="BTC")
    parser.add_argument("--config", help="mass simulation config file", default="")
    parser.add_argument("--title", help="mass simulation title", default="SMA_2H_week")
    parser.add_argument("--offset", help="mass simulation period offset", type=int, default=120)
    parser.add_argument(
        "--mode",
        help="0: interactive simulator, 1: single simulation, 2: real trading",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--from_dash_to",
        help="simulation period ex) 201220.170000-201220.180000",
        default="201220.170000-201220.180000",
    )
    args = parser.parse_args()

    if args.mode < 2:
        simulator = Simulator(
            budget=args.budget,
            interval=args.term,
            strategy=args.strategy,
            currency=args.currency,
            from_dash_to=args.from_dash_to,
        )

    if args.mode == 6:
        parser.print_help()
        sys.exit(0)

    if args.mode == 0:
        simulator.main()
    elif args.mode == 1:
        simulator.run_single()
    elif args.mode == 2:
        controller = Controller(
            budget=args.budget,
            interval=args.term,
            strategy=args.strategy,
            currency=args.currency,
            is_bithumb=args.trader == "1",
        )
        controller.main()
    elif args.mode == 3:
        tcb = TelegramController()
        tcb.main()
    elif args.mode == 4:
        if args.config == "":
            parser.print_help()
            sys.exit(0)

        mass = MassSimulator()
        mass.run(args.config)
    elif args.mode == 5:
        result = MassSimulator.make_config_json(
            title=args.title,
            budget=args.budget,
            strategy_num=args.strategy,
            currency=args.currency,
            from_dash_to=args.from_dash_to,
            offset_min=args.offset,
        )
        print(f"{result} is generated")
