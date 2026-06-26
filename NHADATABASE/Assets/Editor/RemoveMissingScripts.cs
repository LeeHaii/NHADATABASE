using UnityEngine;
using UnityEditor;
using System.Collections.Generic;

public class RemoveMissingScripts
{
    [MenuItem("Tools/Clean Up/1. Remove Missing Scripts In ALL Prefabs")]
    public static void CleanAllPrefabs()
    {
        string[] prefabGuids = AssetDatabase.FindAssets("t:Prefab");
        int goCount = 0;
        int componentsCount = 0;

        EditorUtility.DisplayProgressBar("Cleaning Prefabs", "Scanning all prefabs...", 0f);

        for (int i = 0; i < prefabGuids.Length; i++)
        {
            string path = AssetDatabase.GUIDToAssetPath(prefabGuids[i]);
            GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            
            if (prefab != null)
            {
                EditorUtility.DisplayProgressBar("Cleaning Prefabs", $"Cleaning {prefab.name}...", (float)i / prefabGuids.Length);

                Transform[] children = prefab.GetComponentsInChildren<Transform>(true);
                bool modified = false;
                foreach (Transform child in children)
                {
                    int count = GameObjectUtility.RemoveMonoBehavioursWithMissingScript(child.gameObject);
                    if (count > 0)
                    {
                        goCount++;
                        componentsCount += count;
                        modified = true;
                    }
                }
                
                if (modified)
                {
                    EditorUtility.SetDirty(prefab);
                }
            }
        }
        
        EditorUtility.ClearProgressBar();
        AssetDatabase.SaveAssets();
        Debug.Log($"Success: Removed {componentsCount} missing scripts from {goCount} Prefab GameObjects across the entire project.");
    }

    [MenuItem("Tools/Clean Up/2. Remove Missing Scripts In Active Scene")]
    public static void RemoveInScene()
    {
        int goCount = 0;
        int componentsCount = 0;

        GameObject[] rootObjects = UnityEngine.SceneManagement.SceneManager.GetActiveScene().GetRootGameObjects();
        List<GameObject> allObjects = new List<GameObject>();
        
        foreach (GameObject root in rootObjects)
        {
            Transform[] children = root.GetComponentsInChildren<Transform>(true);
            foreach(Transform t in children) allObjects.Add(t.gameObject);
        }

        Undo.RegisterCompleteObjectUndo(allObjects.ToArray(), "Remove missing scripts");

        foreach (GameObject g in allObjects)
        {
            int count = GameObjectUtility.RemoveMonoBehavioursWithMissingScript(g);
            if (count > 0)
            {
                goCount++;
                componentsCount += count;
                EditorUtility.SetDirty(g);
            }
        }

        Debug.Log($"Success: Removed {componentsCount} missing scripts from {goCount} GameObjects in the active scene.");
    }
}
