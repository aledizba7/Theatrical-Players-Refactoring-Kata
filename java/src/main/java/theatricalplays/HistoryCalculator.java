package theatricalplays;

public class HistoryCalculator extends PlayCalculator {
    public HistoryCalculator(Performance performance, Play play) {
        super(performance, play);
    }

    @Override
    public int amount() {
        int result = 50000;
        if (performance.audience > 30) {
            result += 1500 * (performance.audience - 30);
        }
        return result;
    }

    @Override
    public int volumeCredits() {
        return Math.max(performance.audience - 30, 0) + (int) Math.floor((double) performance.audience / 10);
    }
}
