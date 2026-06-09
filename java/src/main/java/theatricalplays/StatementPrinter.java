package theatricalplays;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class StatementPrinter {

    public String print(Invoice invoice, Map<String, Play> plays) {
        return new PlainTextPrinter().print(createStatementData(invoice, plays));
    }

    public String printHtml(Invoice invoice, Map<String, Play> plays) {
        return new HtmlPrinter().print(createStatementData(invoice, plays));
    }

    private StatementData createStatementData(Invoice invoice, Map<String, Play> plays) {
        List<PerformanceData> performances = invoice.performances.stream()
            .map(perf -> {
                Play play = plays.get(perf.playID);
                PlayCalculator calculator = PlayCalculator.create(perf, play);
                return new PerformanceData(play, perf.audience, calculator.amount(), calculator.volumeCredits());
            })
            .collect(Collectors.toList());

        int totalAmount = performances.stream().mapToInt(PerformanceData::amount).sum();
        int totalVolumeCredits = performances.stream().mapToInt(PerformanceData::credits).sum();

        return new StatementData(invoice.customer, performances, totalAmount, totalVolumeCredits);
    }
}
