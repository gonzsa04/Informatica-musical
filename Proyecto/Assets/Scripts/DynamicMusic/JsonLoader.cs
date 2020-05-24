using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using SimpleJSON;

public class MusicLoader
{
    private static JSONNode rawJson_;

    public static List<List<float>> LoadSong()
    {
        List<List<float>> song = new List<List<float>>();

        for (int i = 0; i < rawJson_[1]["music"].Count; i++)
        {
            List<float> chord = new List<float>();
            for (int j = 0; j < rawJson_[1]["music"][i].Count; j++)
            {
                chord.Add(rawJson_[1]["music"][i][j]);
            }
            song.Add(chord);
        }

        return song;
    }

    public static List<Mode> LoadModes()
    {
        List<Mode> modes = new List<Mode>();

        for(int i = 0; i < rawJson_[2]["modes"].Count; i++)
        {
            Mode mode = new Mode();
            mode.parameters = new List<float>();
            for (int j = 0; j < rawJson_[2]["modes"][i]["params"].Count; j++)
            {
                mode.parameters.Add(rawJson_[2]["modes"][i]["params"][j]);
            }
            modes.Add(mode);
        }

        return modes;
    }
    
    public MusicLoader() {}

    /// <summary>
    /// Establece el json a leer
    /// </summary>
    public static void SetJson(string json)
    {
        rawJson_ = JSON.Parse(json);
    }
}
