from core.run import run

from project.strategy import Strategy


async def main() -> None:
    try:
        run()

        strategy = Strategy(1, 2)

        results: int = strategy.calculate()

        print(results)
    except ModuleNotFoundError:
        print("Module not found")
    except Exception as e:
        print(e)
