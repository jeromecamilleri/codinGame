import com.codingame.gameengine.runner.SoloGameRunner;

// Usage: LocalView "<bot command>" test.json [port]
public class LocalView {
    public static void main(String[] args) {
        SoloGameRunner r = new SoloGameRunner();
        r.setAgent(args[0]);
        r.setTestCase(new java.io.File(args[1]).getAbsoluteFile());
        int port = args.length > 2 ? Integer.parseInt(args[2]) : 8888;
        System.out.println("Ouvrir http://localhost:" + port + "  (Ctrl+C pour arrêter)");
        r.start(port);
    }
}
