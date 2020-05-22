using System.Collections;
using System.Collections.Generic;
using UnityEngine;

struct Mode
{
    public string name;
    public List<float> parameters;

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

    // Start is called before the first frame update
    void Start()
    {
        music = new List<List<float>>();
        modes = new List<Mode>();

        musicIndex = 0;
        modeIndex = 0;

        load();
    }

    private void load()
    {
        Mode mode = new Mode(); mode.init("mode", new List<float>() { 1.0f, 0.5f, 0.0f });
        modes.Add(mode);

        music.Add(new List<float>() { 0, 1, 2 });
        music.Add(new List<float>() { 3, 4, 5 });
        music.Add(new List<float>() { 6, 7, 8 });
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
        
    }
}
