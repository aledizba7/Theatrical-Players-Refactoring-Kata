package theatricalplays;

public abstract class PlayCalculator {
    protected final Performance performance;
    protected final Play play;

    protected PlayCalculator(Performance performance, Play play) {
        this.performance = performance;
        this.play = play;
    }

    public abstract int amount();
    public abstract int volumeCredits();

    public static PlayCalculator create(Performance performance, Play play) {
        return switch (play.type) {
            case "tragedy" -> new TragedyCalculator(performance, play);
            case "comedy" -> new ComedyCalculator(performance, play);
            case "history" -> new HistoryCalculator(performance, play);
            case "pastoral" -> new PastoralCalculator(performance, play);
            default -> throw new Error("unknown type: " + play.type);
        };
    }
}
