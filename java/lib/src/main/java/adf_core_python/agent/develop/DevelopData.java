package adf_core_python.agent.develop;

import jakarta.annotation.Nonnull;

import java.util.List;
import java.util.Map;

public class DevelopData {
    private boolean developFlag = false;

    private Map<String, Integer> intValues;
    private Map<String, Double> doubleValues;
    private Map<String, String> stringValues;
    private Map<String, Boolean> boolValues;

    private Map<String, List<Integer>> intLists;
    private Map<String, List<Double>> doubleLists;
    private Map<String, List<String>> stringLists;
    private Map<String, List<Boolean>> boolLists;

    @Nonnull
    public Integer getInteger(@Nonnull String name, int defaultValue) {
        if (this.developFlag) {
            Integer value = this.intValues.get(name);
            if (value == null) {
                String rawData = this.stringValues.get(name);
                if (rawData != null && !rawData.equals("")) {
                    value = Integer.valueOf(rawData);
                }
                if (value != null) {
                    this.intValues.put(name, value);
                }
            }
            if (value != null) {
                return value;
            }
        }
        return defaultValue;
    }
}
