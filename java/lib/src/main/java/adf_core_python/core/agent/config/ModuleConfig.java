package adf_core_python.core.agent.config;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class ModuleConfig {
    private static final String DEFAULT_CONFIG_FILE_NAME = "../config/module.yaml";
    private final JsonNode rootNode;

    public ModuleConfig() {
        this(DEFAULT_CONFIG_FILE_NAME);
    }

    public ModuleConfig(String configFileName) {
        try {
            String yamlString = Files.readString(Paths.get(configFileName));
            ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
            rootNode = mapper.readTree(yamlString);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public String getValue(String moduleName) {
        String[] keys = moduleName.split("\\.");
        JsonNode moduleNode = rootNode;
        for (String key : keys) {
            if (moduleNode.has(key)) {
                moduleNode = moduleNode.get(key);
            }
        }
        return moduleNode.asText();
    }
}
