public class SoundData
{
    public float volume;
    public float frequency;
    public float pitch;
}

public class SoundDataList
{
    public List<SoundData> soundDataList;
}

public class ScriptData
{
    public string userPrompt;

    public string scriptContent;

    public bool drawUI;
}

public class ScriptDataList
{
    public List<ScriptData> scripts = new List<ScriptData>();
}