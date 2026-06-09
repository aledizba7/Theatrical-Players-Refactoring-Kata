package theatricalplays;

public class ComedyCalculator extends PlayCalculator {
    public ComedyCalculator(Performance performance, Play play) {
        super(performance, play);
    }

    @Override
    public int amount() {
        int result = 30000;
        if (performance.audience > 20) {
            result += 10000 + 500 * (performance.audience - 20);
        }
        result += 300 * performance.audience;
        return result;
    }

    @Override
    public int volumeCredits() {
        return Math.max(performance.audience - 30, 0) + (int) Math.floor((double) performance.audience / 5);
    }
}
