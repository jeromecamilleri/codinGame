import com.codingame.gameengine.runner.SoloGameRunner;
import com.codingame.gameengine.runner.simulate.GameResult;

// Usage: LocalBatch "<bot command>" test1.json [test2.json ...]
public class LocalBatch {
    public static void main(String[] args) {
        String cmd = args[0];
        for (int i = 1; i < args.length; i++) {
            SoloGameRunner r = new SoloGameRunner();
            r.setAgent(cmd);
            r.setTestCase(new java.io.File(args[i]).getAbsoluteFile());
            GameResult g = r.simulate();
            String s = g.metadata;
            String err = g.failCause == null ? "" : " FAIL=" + g.failCause;
            System.out.println("RESULT " + args[i] + " score=" + s + err);
            if (g.summaries != null) for (String l : g.summaries) if (l != null && l.contains("arn")) System.out.println("  WARN " + l.replace("\n"," | "));
            if (System.getenv("DUMP") != null && g.outputs != null) for (var o : g.outputs.entrySet()) System.out.println("  OUT " + o.getKey() + " n=" + o.getValue().size() + " first=" + o.getValue().subList(0, Math.min(3, o.getValue().size())));
            if (g.errors != null) {
                for (var e : g.errors.entrySet()) {
                    for (String l : e.getValue()) {
                        if (l != null && !l.isEmpty()) System.out.println("  ERR " + l);
                    }
                }
            }
        }
        System.exit(0);
    }
}
