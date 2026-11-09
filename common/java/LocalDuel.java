import com.codingame.gameengine.runner.MultiplayerGameRunner;
import com.codingame.gameengine.runner.simulate.GameResult;

// Usage: LocalDuel view|batch leagueLevel seed port "<cmd bot0>" "<cmd bot1>"
public class LocalDuel {
    public static void main(String[] args) {
        String mode = args[0];
        MultiplayerGameRunner r = new MultiplayerGameRunner();
        r.setLeagueLevel(Integer.parseInt(args[1]));
        r.setSeed(Long.parseLong(args[2]));
        r.addAgent(args[4], "bot0");
        r.addAgent(args[5], "bot1");
        if (mode.equals("view")) {
            System.out.println("Ouvrir http://localhost:" + args[3] + "/test.html  (Ctrl+C pour arrêter)");
            r.start(Integer.parseInt(args[3]));
            return;
        }
        GameResult g = r.simulate();
        System.out.println("RESULT seed=" + args[2] + " scores=" + g.scores + (g.failCause == null ? "" : " FAIL=" + g.failCause));
        System.exit(0);
    }
}
