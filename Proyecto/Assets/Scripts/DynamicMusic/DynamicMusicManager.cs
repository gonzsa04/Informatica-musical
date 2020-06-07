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
    //lista de acordes, cada uno una lista de notas formando asi la cancion deseada
    static private List<List<float>> song;
    //lista de modos posibles, de mas alegre a mas tenebroso
    static private List<Mode> modes;
    //acorde actual de la cancion de ambiente
    static private int ambientMusicIndex;
    //modo actual de la musica dinamica
    static private int modeIndex;

    //intervalos para saber cuanto aumentar de modo segun el 
    //numero de enemigos, energia y joyas restantes
    private float enemyModeInterval;
    private float energyModeInterval;
    private float joyasModeInterval;
    private PlayerController playerController;

    public GameObject player;
    public Transform enemyPos;
    public TextAsset jsonFile;

    void Start()
    {
        ambientMusicIndex = 0;
        modeIndex = 0;

        //leemos y cargamos la musica y los modos
        MusicLoader.SetJson(jsonFile.text);
        load();

        playerController = player.GetComponent<PlayerController>();

        //calculamos el valor de cada salto entre modos
        enemyModeInterval = Vector3.Distance(player.transform.position, enemyPos.position) / modes.Count;
        energyModeInterval = (float)(playerController.maxEnergia) / modes.Count;
        joyasModeInterval = (float)(GameManager.instance.joyasTotales) / modes.Count;

        //se toca un acorde de la musica de ambiente cada 0.6 segundos
        InvokeRepeating("playAmbient", 0.0f, 0.6f);
    }

    private void load()
    {
        song = MusicLoader.LoadSong();
        modes = MusicLoader.LoadModes();
    }

    public static void play()
    {
        //decimos a Supercollider que cargue el acorde en concreto
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadNote", modes[modeIndex].chord);
        //a continuacion que carge los parametros del modo actual
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadParams", modes[modeIndex].parameters);
        //y al final que haga sonar el acorde
        OSCHandler.Instance.SendMessageToClient<float>("SuperCollider", "/notePlay", 0.4f);
    }
    
    void Update()
    {
        //en cada frame, calculamos cuan tensa es la situacion del jugador fijandonos 
        //en el enemigo, la energia y joyas restantes
        float enemyMode = modes.Count - (Vector3.Distance(player.transform.position, enemyPos.position) / enemyModeInterval);
        float energyMode = modes.Count - (playerController.energia / energyModeInterval);
        float joyasMode = playerController.numJoyasRecogidas / joyasModeInterval;

        //cada una de estas variables tiene un peso diferente a la hora de afectar
        //al modo en el que se tocan los acordes
        modeIndex = (int)((energyMode * 1.0/3.0) + (enemyMode * 1.0/2.0) + (joyasMode * 1.0/6.0));

        Debug.Log(modeIndex);
    }

    private void playAmbient()
    {
        //decimos a Supercollider que cargue el acorde en concreto
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadNote", song[ambientMusicIndex]);
        //a continuacion que carge los parametros del modo actual
        OSCHandler.Instance.SendMessagesToClient<float>("SuperCollider", "/loadParams", modes[modeIndex].parameters);
        //y al final que haga sonar el acorde
        OSCHandler.Instance.SendMessageToClient<float>("SuperCollider", "/degreePlay", 0.2f);

        //avanzamos en la cancion (siguiente acorde)
        ambientMusicIndex++;
        if (ambientMusicIndex >= song.Count) ambientMusicIndex = 0;
    }
}
