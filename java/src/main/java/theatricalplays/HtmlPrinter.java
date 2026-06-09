package theatricalplays;

import java.text.NumberFormat;
import java.util.Locale;

public class HtmlPrinter implements Printer {
    @Override
    public String print(StatementData data) {
        StringBuilder result = new StringBuilder(String.format("<h1>Statement for %s</h1>%n", data.customer()));
        result.append("<table>%n".formatted());
        result.append("<tr><th>play</th><th>seats</th><th>cost</th></tr>%n".formatted());
        NumberFormat frmt = NumberFormat.getCurrencyInstance(Locale.US);

        for (var perf : data.performances()) {
            result.append(String.format("  <tr><td>%s</td><td>%s</td><td>%s</td></tr>%n", perf.play().name, perf.audience(), frmt.format((double) perf.amount() / 100)));
        }
        result.append("</table>%n".formatted());
        result.append(String.format("<p>Amount owed is <em>%s</em></p>%n", frmt.format((double) data.totalAmount() / 100)));
        result.append(String.format("<p>You earned <em>%s</em> credits</p>%n", data.totalVolumeCredits()));
        return result.toString();
    }
}
