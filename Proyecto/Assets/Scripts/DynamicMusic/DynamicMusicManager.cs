using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public struct Mode
{
    public List<float> parameters; // DUR, AMP, SCALE, OCTAVE
    public List<float> chord;      // acorde
}

public class DynamicMusicManager : MonoBehaviour
{
    static private List<List<float>> song;
    static private List<Mode> modes;
    static private int musicIndex;
    static private int ambientMusicIndex;
    static private int modeIndex;

    private float enemyModeInterval;
    private float energyModeInterval;
    private float joyasModeInterval;
    private PlayerController playerController;

    public GameObject player;
    public Transform enemyPos;
    public TextAsset jsonFile;

    // Start is called before the first frame update
    void Start()
    {
        musicIndex = 0;
        ambientMusicIndex = 0;
        modeIndex = 0;

        MusicLoader.SetJson(jsonFile.text);
        load();

        playerController = player.GetComponent<PlayerController>();

        enemyModeInterval = Vector3.Distance(player.transform.position, enemyPos.position) / modes.Count;
        energyModeInterval = (float)(playerController.maxEnergia) / modes.Count;
        joyasModeInterval = (float)(GameManager.instance.joyasTotales) / modes.Count;

        InvokeRepeating("playAmbient", 0.0f, 0.6f);
    }

    private void load()
    {
        song = MusicLoader.LoadSong();
        modes = MusicLoader.LoadModes();
    }

    public static void play()
    {
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadNote", modes[modeIndex].chord);
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadParams", modes[modeIndex].parameters);
        OSCHandler.Instance.SendMessageToClient<float>("SuperCollider", "/notePlay", 0.4f);

        musicIndex++;
        if (musicIndex >= song.Count) musicIndex = 0;
    }

    // Update is called once per frame
    void Update()
    {
        float enemyMode = modes.Count - (Vector3.Distance(player.transform.position, enemyPos.position) / enemyModeInterval);
        float energyMode = modes.Count - (playerController.energia / energyModeInterval);
        float joyasMode = playerController.numJoyasRecogidas / joyasModeInterval;

        modeIndex = (int)((energyMode * 1.0/3.0) + (enemyMode * 1.0/2.0) + (joyasMode * 1.0/6.0));

        Debug.Log(modeIndex);
    }

    private void playAmbient()
    {
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadNote", song[ambientMusicIndex]);
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadParams", modes[modeIndex].parameters);
        OSCHandler.Instance.SendMessageToClient<float>("SuperCollider", "/degreePlay", 0.2f);

        ambientMusicIndex++;
        if (ambientMusicIndex >= song.Count) ambientMusicIndex = 0;
    }
}
