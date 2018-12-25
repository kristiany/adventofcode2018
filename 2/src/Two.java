import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Two {

    private int checksum(final List<String> input) {
        return input
                .stream()
                .flatMap(this::twosAndThrees)
                .reduce(Result::add)
                .orElse(new Result(0, 0))
                .checksum();
    }

    private Map<Character, Integer> frequencyMap(final String input) {
        final Map<Character, Integer> result = new HashMap<>();
        for(int i = 0; i < input.length(); ++i) {
            final char c = input.charAt(i);
            if(result.containsKey(c)) {
                result.put(c, result.get(c) + 1);
            }
            else {
                result.put(c, 1);
            }
        }
        return result;
    }

    private Stream<Result> twosAndThrees(final String input) {
        final Map<Character, Integer> multiples = frequencyMap(input);
        final boolean twos = multiples.values().stream()
                .anyMatch(v -> v == 2);
        final boolean threes = multiples.values().stream()
                .anyMatch(v -> v == 3);
        return Stream.of(new Result(twos ? 1 : 0, threes ? 1 : 0));
    }

    private String similar(final List<String> input) {
        for(int ref = 0; ref < input.size() - 1; ++ref) {
            for(int i = ref + 1; i < input.size(); ++i) {
                final int one = oneOff(input.get(ref), input.get(i));
                if(one >= 0) {
                    return input.get(ref).substring(0, one) + input.get(ref).substring(one + 1);
                }
            }
        }
        return null;
    }

    private int oneOff(final String a, final String b) {
        int index = -1;
        for(int i = 0; i < a.length(); ++i) {
            if(a.charAt(i) != b.charAt(i)) {
                if(index >= 0) {
                    return -1;
                }
                index = i;
            }
        }
        return index;
    }

    public static void main(final String[] args) {
        final List<String> testInput1 = Arrays.asList(
                "abcdef",
                "bababc",
                "abbcde",
                "abcccd",
                "aabcdd",
                "abcdee",
                "ababab"
        );
        final Two two = new Two();
        System.out.printf("Part 1: test checksum is %d\n", two.checksum(testInput1));
        System.out.printf("Part 1: checksum is %d\n", two.checksum(input()));
        final List<String> testInput2 = Arrays.asList(
                "abcde",
                "fghij",
                "klmno",
                "pqrst",
                "fguij",
                "axcye",
                "wvxyz"
        );
        System.out.printf("Part 2: test similar letters: %s\n", two.similar(testInput2));
        System.out.printf("Part 2: the two box IDs similar letters: %s\n", two.similar(input()));
    }

    static List<String> input() {
        try(final BufferedReader r = new BufferedReader(new FileReader("input.txt"))) {
            return r.lines().collect(Collectors.toList());
        }
        catch(final IOException e) {
            throw new RuntimeException(e);
        }
    }

    static class Result {
        private final int twos;
        private final int threes;

        Result(final int twos, final int threes) {
            this.twos = twos;
            this.threes = threes;
        }

        Result add(final Result other) {
            return new Result(this.twos + other.twos, this.threes + other.threes);
        }

        int checksum() {
            System.out.println(this.twos + " * " + this.threes + " = " + this.twos * this.threes);
            return this.twos * this.threes;
        }
    }
}


