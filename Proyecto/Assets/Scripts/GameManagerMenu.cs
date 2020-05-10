using UnityEngine;
using System.Collections;

public class GameManagerMenu : MonoBehaviour {

    public GameObject botonInicio, botonCreditos, botonSalir, textoCreditos;

	public void comenzarNivel(){//se hace al pulsar jugar
		Application.LoadLevel ("Game");//carga el nivel
	}

    public void creditos()//se hace al pulsar creditos
    {
        botonInicio.SetActive(false);
        botonCreditos.SetActive(false);
        botonSalir.SetActive(true);
        textoCreditos.SetActive(true);
    }

    public void salir()//se hace al pulsar salir
    {
        botonInicio.SetActive(true);
        botonCreditos.SetActive(true);
        botonSalir.SetActive(false);
        textoCreditos.SetActive(false);
    }
}
