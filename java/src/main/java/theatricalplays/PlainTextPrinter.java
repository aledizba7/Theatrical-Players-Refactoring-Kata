package theatricalplays;

import java.text.NumberFormat;
import java.util.Locale;

public class PlainTextPrinter implements Printer {
    @Override
    public String print(StatementData data) {
        StringBuilder result = new StringBuilder(String.format("Statement for %s%n", data.customer()));
        NumberFormat frmt = NumberFormat.getCurrencyInstance(Locale.US);

        for (var perf : data.performances()) {
            result.append(String.format("  %s: %s (%s seats)%n", perf.play().name, frmt.format((double) perf.amount() / 100), perf.audience()));
        }
        result.append(String.format("Amount owed is %s%n", frmt.format((double) data.totalAmount() / 100)));
        result.append(String.format("You earned %s credits%n", data.totalVolumeCredits()));
        return result.toString();
    }
}
