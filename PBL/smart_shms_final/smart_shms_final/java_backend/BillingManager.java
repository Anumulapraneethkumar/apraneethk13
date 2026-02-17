import java.util.*;
public class BillingManager {
    static Stack<String> stack = new Stack<>();
    public static void main(String[] args) throws Exception {
        if (args.length==0) { System.out.println(""); return; }
        String cmd = args[0];
        if (cmd.equals("push") && args.length>1) {
            stack.push(args[1]);
            System.out.println("Pushed");
        } else if (cmd.equals("pop")) {
            if (stack.empty()) System.out.println("");
            else System.out.println(stack.pop());
        } else System.out.println("Unknown");
    }
}
