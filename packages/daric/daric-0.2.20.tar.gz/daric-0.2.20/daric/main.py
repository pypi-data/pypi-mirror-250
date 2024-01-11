import typer
import daric.lib.calculation
import daric.lib.normalization
import daric.lib.hmm

app = typer.Typer()
app.command()(daric.lib.calculation.calculate)
app.command()(daric.lib.normalization.normalize)
app.command()(daric.lib.hmm.runhmm)


if __name__ == "__main__":
    app()