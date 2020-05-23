using System.Collections;
using System.Collections.Generic;
using UnityEngine;

struct Mode
{
    public string name;
    public List<float> parameters; // DUR, AMP, SCALE, OCTAVE

    public void init(string name, List<float> parameters)
    {
        this.name = name;
        this.parameters = parameters;
    }
}

public class DynamicMusicManager : MonoBehaviour
{
    static private List<List<float>> music;
    static private List<Mode> modes;
    static private int musicIndex;
    static private int modeIndex;

    private float enemyModeInterval;
    private float energyModeInterval;
    private float joyasModeInterval;
    private PlayerController playerController;

    public GameObject player;
    public Transform enemyPos;

    // Start is called before the first frame update
    void Start()
    {
        music = new List<List<float>>();
        modes = new List<Mode>();

        musicIndex = 0;
        modeIndex = 0;

        load();

        playerController = player.GetComponent<PlayerController>();

        enemyModeInterval = Vector3.Distance(player.transform.position, enemyPos.position) / modes.Count;
        energyModeInterval = (float)(playerController.maxEnergia) / modes.Count;
        joyasModeInterval = (float)(GameManager.instance.joyasTotales) / modes.Count;
    }

    private void load()
    {
        Mode mode = new Mode(); mode.init("mode", new List<float>() { 1.0f, 0.5f, 0.0f, 5.0f });
        Mode mode2 = new Mode(); mode2.init("mode", new List<float>() { 1.0f, 0.5f, 0.0f, 6.0f });
        Mode mode3 = new Mode(); mode3.init("mode", new List<float>() { 0.7f, 0.5f, 0.0f, 6.0f });
        Mode mode4 = new Mode(); mode4.init("mode", new List<float>() { 0.7f, 0.5f, 0.0f, 7.0f });
        Mode mode5 = new Mode(); mode5.init("mode", new List<float>() { 0.5f, 0.5f, 1.0f, 7.0f });
        Mode mode6 = new Mode(); mode6.init("mode", new List<float>() { 0.5f, 0.8f, 1.0f, 8.0f });
        Mode mode7 = new Mode(); mode7.init("mode", new List<float>() { 0.3f, 1.0f, 1.0f, 8.0f });
        Mode mode8 = new Mode(); mode8.init("mode", new List<float>() { 0.3f, 1.0f, 1.0f, 8.0f });
        modes.Add(mode);
        modes.Add(mode2);
        modes.Add(mode3);
        modes.Add(mode4);
        modes.Add(mode5);
        modes.Add(mode6);
        modes.Add(mode7);
        modes.Add(mode8);

        music.Add(new List<float>() { 0, 1 });
        music.Add(new List<float>() { 2, 3 });
        music.Add(new List<float>() { 4, 5 });
        music.Add(new List<float>() { 6, 7 });
        music.Add(new List<float>() { 8, 9 });
    }

    public static void play()
    {
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadNote", music[musicIndex]);
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadParams", modes[modeIndex].parameters);
        OSCHandler.Instance.SendMessageToClient<float>("SuperCollider", "/play", 0.0f);

        musicIndex++;
        if (musicIndex >= music.Count) musicIndex = 0;
    }

    // Update is called once per frame
    void Update()
    {
        float enemyMode = modes.Count - (Vector3.Distance(player.transform.position, enemyPos.position) / enemyModeInterval);
        float energyMode = modes.Count - (playerController.energia / energyModeInterval);
        float joyasMode = playerController.numJoyasRecogidas / joyasModeInterval;

        modeIndex = (int)((energyMode + energyMode + joyasMode) / 3);

        Debug.Log(modeIndex);
    }
}
