// ----------------------------------------------------------
// Material adicional de la práctica 3.
// Motores de Videojuegos - FDI - UCM
// ----------------------------------------------------------
// Profesor: Marco Antonio Gómez Martín
// ----------------------------------------------------------
using UnityEngine;
using System.Collections;

/// <summary>
/// Componente utilizado para hacer que la cámara se mueva
/// hasta una posición fija configurable desde el editor.
/// </summary>
/// 
/// Cuando se activa el componente, se inicia un movimiento
/// del GO al que pertenece hasta que alcanza esa posición
/// (y orientación).
/// 
/// Se puede ocnfigurar desde el editor el nivel de suavizado.
/// 
/// Además, hace esfuerzos por mantener el target a la vista. Si
/// se pone algo delante, le envía el mensaje "ActivaTransparencia",
/// con la esperanza de que se vuelva transparente.
public class FixedCamera : MonoBehaviour {

    public Transform location;

	public float smoothLevel;

	/// <summary>
	/// Método que hace la actualización de la posición, mirando la posición del target
	/// y cambiando (suavizando) la posición de la cámara.
	/// </summary>
	void LateUpdate()
	{
		// Movemos la cámara
		transform.position = Vector3.Lerp(
			transform.position, location.position, Time.deltaTime * smoothLevel);

		// Y la orientacion
		Quaternion targetRot = location.rotation;

		// Lerp the camera's rotation between it's current rotation and the rotation that looks at the player.
		transform.rotation = Quaternion.Lerp(transform.rotation, targetRot, smoothLevel * Time.deltaTime);
	}
}
