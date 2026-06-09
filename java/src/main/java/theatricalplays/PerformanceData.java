package theatricalplays;

public record PerformanceData(
    Play play,
    int audience,
    int amount,
    int credits
) {}
