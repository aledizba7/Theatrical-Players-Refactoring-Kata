package theatricalplays;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.approvaltests.Approvals.verify;
import static org.junit.jupiter.api.Assertions.assertEquals;

class StatementPrinterTests {

    @Test
    void exampleStatement() {
        Map<String, Play> plays = Map.of(
                "hamlet",  new Play("Hamlet", "tragedy"),
                "as-like", new Play("As You Like It", "comedy"),
                "othello", new Play("Othello", "tragedy"));

        Invoice invoice = new Invoice("BigCo", List.of(
                new Performance("hamlet", 55),
                new Performance("as-like", 35),
                new Performance("othello", 40)));

        StatementPrinter statementPrinter = new StatementPrinter();
        var result = statementPrinter.print(invoice, plays);

        verify(result);
    }

    @Test
    void statementWithNewPlayTypes() {
        Map<String, Play> plays = Map.of(
                "henry-v",  new Play("Henry V", "opera"),
                "as-like", new Play("As You Like It", "musical"));

        Invoice invoice = new Invoice("BigCo", List.of(
                new Performance("henry-v", 53),
                new Performance("as-like", 55)));

        StatementPrinter statementPrinter = new StatementPrinter();
        Error error = Assertions.assertThrows(Error.class,
            () -> statementPrinter.print(invoice, plays));
        assertEquals("unknown type: opera", error.getMessage());
    }

    @Test
    void htmlStatement() {
        Map<String, Play> plays = Map.of(
                "hamlet",  new Play("Hamlet", "tragedy"),
                "as-like", new Play("As You Like It", "comedy"),
                "othello", new Play("Othello", "tragedy"));

        Invoice invoice = new Invoice("BigCo", List.of(
                new Performance("hamlet", 55),
                new Performance("as-like", 35),
                new Performance("othello", 40)));

        StatementPrinter statementPrinter = new StatementPrinter();
        var result = statementPrinter.printHtml(invoice, plays);

        String expected = "<h1>Statement for BigCo</h1>\n" +
                "<table>\n" +
                "<tr><th>play</th><th>seats</th><th>cost</th></tr>\n" +
                "  <tr><td>Hamlet</td><td>55</td><td>$650.00</td></tr>\n" +
                "  <tr><td>As You Like It</td><td>35</td><td>$580.00</td></tr>\n" +
                "  <tr><td>Othello</td><td>40</td><td>$500.00</td></tr>\n" +
                "</table>\n" +
                "<p>Amount owed is <em>$1,730.00</em></p>\n" +
                "<p>You earned <em>47</em> credits</p>\n";

        String normalizedResult = result.replace("\r\n", "\n");
        assertEquals(expected, normalizedResult);
    }

    @Test
    void testTragedyCalculator() {
        Play play = new Play("Hamlet", "tragedy");
        
        TragedyCalculator calcSmall = new TragedyCalculator(new Performance("hamlet", 20), play);
        assertEquals(40000, calcSmall.amount());
        assertEquals(0, calcSmall.volumeCredits());

        TragedyCalculator calcLarge = new TragedyCalculator(new Performance("hamlet", 35), play);
        assertEquals(45000, calcLarge.amount());
        assertEquals(5, calcLarge.volumeCredits());
    }

    @Test
    void testComedyCalculator() {
        Play play = new Play("As You Like It", "comedy");
        
        ComedyCalculator calcSmall = new ComedyCalculator(new Performance("as-like", 15), play);
        assertEquals(34500, calcSmall.amount());
        assertEquals(3, calcSmall.volumeCredits());

        ComedyCalculator calcLarge = new ComedyCalculator(new Performance("as-like", 25), play);
        assertEquals(50000, calcLarge.amount());
        assertEquals(5, calcLarge.volumeCredits());
    }

    @Test
    void testHistoryCalculator() {
        Play play = new Play("Henry V", "history");
        
        HistoryCalculator calcSmall = new HistoryCalculator(new Performance("henry-v", 20), play);
        assertEquals(50000, calcSmall.amount());
        assertEquals(2, calcSmall.volumeCredits());

        HistoryCalculator calcLarge = new HistoryCalculator(new Performance("henry-v", 35), play);
        assertEquals(57500, calcLarge.amount());
        assertEquals(8, calcLarge.volumeCredits());
    }

    @Test
    void testPastoralCalculator() {
        Play play = new Play("As You Like It", "pastoral");
        
        PastoralCalculator calcSmall = new PastoralCalculator(new Performance("as-like", 10), play);
        assertEquals(25000, calcSmall.amount());
        assertEquals(1, calcSmall.volumeCredits());

        PastoralCalculator calcLarge = new PastoralCalculator(new Performance("as-like", 20), play);
        assertEquals(29000, calcLarge.amount());
        assertEquals(2, calcLarge.volumeCredits());
    }
}
