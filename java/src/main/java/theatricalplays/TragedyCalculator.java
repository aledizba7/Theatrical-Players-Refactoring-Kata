package theatricalplays;

public class TragedyCalculator extends PlayCalculator {
    public TragedyCalculator(Performance performance, Play play) {
        super(performance, play);
    }

    @Override
    public int amount() {
        int result = 40000;
        if (performance.audience > 30) {
            result += 1000 * (performance.audience - 30);
        }
        return result;
    }

    @Override
    public int volumeCredits() {
        return Math.max(performance.audience - 30, 0);
    }
}
