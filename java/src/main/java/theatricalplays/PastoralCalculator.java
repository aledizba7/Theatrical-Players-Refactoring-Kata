package theatricalplays;

public class PastoralCalculator extends PlayCalculator {
    public PastoralCalculator(Performance performance, Play play) {
        super(performance, play);
    }

    @Override
    public int amount() {
        int result = 25000;
        if (performance.audience > 15) {
            result += 800 * (performance.audience - 15);
        }
        return result;
    }

    @Override
    public int volumeCredits() {
        return Math.max(performance.audience - 30, 0) + (int) Math.floor((double) performance.audience / 8);
    }
}
