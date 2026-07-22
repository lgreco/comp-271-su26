// Quick demo of the `final` keyword: once a final variable is assigned,
// the compiler rejects any later attempt to reassign it. Unlike Python's
// "we are all adults here" convention (e.g. ALL_CAPS names), this is
// enforced at compile time, not just a naming convention.
public class Final {

    public static void main(String[] args) {
        final int x = 5;
        // This reassignment does not compile: javac reports
        // "error: cannot assign a value to final variable x"
        // and refuses to build the program.
        x = x+5;
        System.out.println(x);
    }
}
