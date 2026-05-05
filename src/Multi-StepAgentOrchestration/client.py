import argparse
import asyncio
import json

from orchestrator import run_bid_proposal
from models import ProposalPhase


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bid-proposal orchestration client")
    parser.add_argument("client", type=str, help="Client name to research/process")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    ctx = asyncio.run(run_bid_proposal(client_name=args.client))

    print(
        json.dumps(
            {
                "phase": ProposalPhase.DRAFTED,
                "research": ctx.research,
                "draft": ctx.draft,
                "processed": ctx.processed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
