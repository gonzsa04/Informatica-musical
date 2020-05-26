using UnityEngine;
using System.Collections;
using System;

public class PlayerController : MonoBehaviour {
	// Use this for initialization
	public int energia=100;//energia total
    public int maxEnergia = 100;
	public int numJoyas=0;//joyas portadas
	public int numJoyasRecogidas=0;//joyas portadas
	GameObject nuevaJoya;
    public GameObject Joya;
    public GameObject muro;
    public GameObject exit;
    public GameObject topCamera;
    public GameObject MainCamara;
    public Transform posCamara;
	void Start () {

	}

	// Update is called once per frame
	void Update () {
        GameManager.instance.UpdateGUI();//actualiza el GUI
		PlayerMovement ();
		LogicaJoya ();
		if (energia == 0)
			GameManager.instance.GameOver ();   
	}

    void PlayerMovement(){//gestiona el movimiento
		if (Input.GetKeyDown (KeyCode.W) && (Physics.Raycast (this.transform.position, this.transform.forward, 0.75f) != muro.gameObject)) {//si pulsamos w y no hay muro delante
			this.transform.position += this.transform.forward;//se mueve hacia donde estemos mirando
			energia -= (1 + numJoyas);//la energia se restara en funcion de los movimientos y del num de joyas portadas

            DynamicMusicManager.play();
        }
        else if (Input.GetKeyDown (KeyCode.A))//si pulsamos a
			this.transform.Rotate (new Vector3 (0, -90, 0));//gira hacia la izq 90 grados
		else if (Input.GetKeyDown (KeyCode.D))//si pulsamos la d
			this.transform.Rotate (new Vector3 (0, 90, 0));//gira hacia la derecha 90 grados
		else if (Input.GetKeyDown (KeyCode.W) && (Physics.Raycast (this.transform.position, this.transform.forward, 0.4f) == exit.gameObject)) { //si colisionas con la salida
			GameManager.instance.Exit (); //llamamos a exit
			Reset (); //se invoca al reset
		}
        else if(Input.GetKeyDown(KeyCode.M) && (energia - 10 > 0))//si pulsas m y tienes suficiente energia
        {
            MapCamera();
        }
      }

	void LogicaJoya(){//gestiona joyas que cogemos/soltamos
        if (Input.GetKeyDown(KeyCode.C) && energia > 20 * (1 + numJoyas))
        {//si pulsamos c y la energia nos lo permite
            cogeJoya();//llamamos a cogejoya
        }
        else if (Input.GetKeyDown(KeyCode.Z) || energia < 20 * numJoyas)//si pulsamos z o nuestra energia es muy baja
            sueltaJoya();//llamamos a sueltajoya
	}

	void cogeJoya(){
		Collider[]coll=Physics.OverlapSphere(this.transform.position,1);//hace un array de colisiones en una circunferencia de radio 1
		for (int i = 0; i < coll.Length; i++)//recorremos el array
			if (coll [i].CompareTag ("Joya")) {//si un elemento del array tiene tag joya
				Destroy(coll[i].gameObject);//se destruye ese gameobject(nos le guardamos)
				numJoyas++;//aumenta el numero de joyas cogidas en uno
                numJoyasRecogidas++;

                float coge = 1.0f;
                OSCHandler.Instance.SendMessageToClient<float>("SuperCollider", "/coge", coge);
                Debug.Log("coge");
            }
	}
    void sueltaJoya()
    {
        if (numJoyas > 0)
        {//si tenemos mas de una joya
            nuevaJoya = Instantiate(Joya);//hacemos aparecer una joya
            nuevaJoya.transform.position = this.transform.position;//la colocamos en la posicion del jugador
            numJoyas--;//disminuye el numero de joyas en uno
            numJoyasRecogidas--;
            
            OSCHandler.Instance.SendMessageToClient<float>("SuperCollider", "/coge", 1.0f);
            Debug.Log("coge");
        }
    }

    public void Reset() {//repone la energia y te quita las joyas
            energia = maxEnergia;
            numJoyas = 0;
            this.transform.position = exit.transform.position+exit.transform.forward;
            this.transform.rotation = exit.transform.rotation;//se pone al jugador uno mas alante que la posicion de exit, con su misma rotacion 
	}

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Fantasma"))
        { //si colisiona con un objeto con tag fantasma
            OSCHandler.Instance.SendMessageToClient<float>("SuperCollider", "/muere", 1.0f);
            GameManager.instance.GameOver(); //invoca al gameover
        }
    }

    void MapCamera()//al pulsar M
    {
        energia -= 10;//resta energia
        GetComponent<PlayerController>().enabled = false;//te quita el movimiento
        topCamera.transform.position = MainCamara.transform.position;
        topCamera.SetActive(true);//se activa la camara de arriba
        MainCamara.SetActive(false);
        Invoke("EndMapCamera", 2f);//en dos segundos se llama a endmapcamera
    }

    void EndMapCamera()
    {
        MainCamara.transform.position = posCamara.transform.position;
        MainCamara.SetActive(true);//se activa la camara del jugador
        topCamera.SetActive(false);
        GetComponent<PlayerController>().enabled = true;//te devuelve el movimiento
    }
}

