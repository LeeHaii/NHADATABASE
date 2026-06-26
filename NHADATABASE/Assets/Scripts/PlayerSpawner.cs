using UnityEngine;

public class PlayerSpawner : MonoBehaviour
{
    public GameObject playerPrefab;

    void Awake()
    {
        if (playerPrefab != null)
        {
            // Spawn the player
            Instantiate(playerPrefab, transform.position, transform.rotation);
        }
        else
        {
            Debug.LogError("PlayerSpawner: Player Prefab is not assigned.");
        }
    }
}
