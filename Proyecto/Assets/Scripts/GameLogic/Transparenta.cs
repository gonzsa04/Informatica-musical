using UnityEngine;
using System.Collections;

public class Transparenta : MonoBehaviour {
    public Renderer r;//aqui arrastraremos el renderer del cubo que tiene al muro
    bool transparenta = false;
    // Use this for initialization
    void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
        if (transparenta)//si transparencia true
        {
            Color c = r.material.color;
            c.a = 0.5f;//se cambia la transparencia del objeto(muro)
            r.material.color = c;
            transparenta = false;
        }
        else//si transparencia false
        {
            Color c2 = r.material.color;
            c2.a = 1;//se mantiene la transparencia en el estado inicial
            r.material.color = c2;
        }
    }
    public void ActivaTransparencia()//sera llamado mediante un mensaje enviado por la camara. Al responder ese mensaje ejecuta este codigo
    {
        transparenta = true;
    }

}
