import java.util.*;
public class AppointmentManager {
    static Queue<String> q = new LinkedList<>();
    public static void main(String[] args) {
        if (args.length==0) { System.out.println("No args"); return; }
        String cmd = args[0];
        if (cmd.equals("add") && args.length>1) {
            q.add(args[1]);
            System.out.println("Added");
        } else if (cmd.equals("view")) {
            for (String s:q) System.out.println(s);
        } else {
            System.out.println("Unknown");
        }
    }
}
