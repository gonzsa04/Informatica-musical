using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class GameManager : MonoBehaviour {
	public static GameManager instance;//permite llamar a metodos del gamemanager desde otros componentes
	PlayerController nuevo;
	BoxCollider parar;
	public UnityEngine.UI.Text textoEnergia, textoJoyas, textoGanarPerder, textovolvermenu;//UI
	public GameObject tryAgain, exit, volvermenu;
	int joyasTotales;

	// Use this for initialization
	void Start () {
		instance = this;
		nuevo = GameObject.FindWithTag("Player").GetComponent<PlayerController> ();//encuentra el objeto con tag player y usa su componente playercontroller
        joyasTotales = GameObject.FindGameObjectsWithTag("Joya").Length;//encuentra objetos con tag joya
        parar = GameObject.FindWithTag("Player").GetComponent<BoxCollider> ();//encuentra el objeto con tag player y usa su componente boxcollider
	}
	
	public void UpdateGUI(){
		textoEnergia.text = ("Energía: " + nuevo.energia);//energia que queda
		textoJoyas.text = ("Joyas restantes: " + (joyasTotales-nuevo.numJoyas));//joyas que quedan por coger
	}
	public void GameOver(){//se llama desde playercontroller cuando el jugador choca con el fantasma
        nuevo.enabled = false; //quitamos el movimiento al jugador
        tryAgain.SetActive (true);//se activa el boton para volver a cargar el nivel
		textoGanarPerder.text = ("Has perdido!");
	}
	public void Exit(){//se llama desde playercontroler cuando el jugador choca con la salida
		parar.enabled = false; //quitamos el collider al jugador para que no colisione con el fantasma
        nuevo.enabled = false; //quitamos el movimiento al jugador
		if (joyasTotales - nuevo.numJoyas == 0) {//si todas las joyas estan recogidas
			volvermenu.SetActive (true); //se activa el UI para volver al menu
			textoGanarPerder.color = Color.green;
			textoGanarPerder.text = ("Has ganado!");
		}
		else if (joyasTotales - nuevo.numJoyas != 0)  { // si faltan joyas por recoger
			joyasTotales -= nuevo.numJoyas;
			exit.SetActive (true);   //se activa el UI de volver a entrar
		}

	}
	public void resetNivel (){ //lo hace el boton try again
		Application.LoadLevel ("Game"); //se resetea la escena
	}
	public void moverJugador(){ //al pulsar el boton de volver a entrar
		parar.enabled = true; //te pone el collider
		nuevo.enabled = true; //te deja moverte
		exit.SetActive (false); //se quita el boton
	}
	public void volverMenu(){//lo hace el boton volver al menu
		Application.LoadLevel ("Menu");
	}
}
