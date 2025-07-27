package test.java;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.And;
import io.cucumber.datatable.DataTable;
import org.junit.jupiter.api.Assertions;
import main.java.OrderService;
import java.util.*;

public class OrderStepDefs {
    List<Map<String, String>> orderItems;
    int totalAmount;
    OrderService orderService = new OrderService();
    int threshold;
    int discount;
    int originalAmount;
    Map<String, Integer> summary;
    boolean bogoCosmeticsActive;
    Map<String, Object> bogoResult;
    Map<String, Object> stackedResult;
    Map<String, Object> thresholdResult;
    Map<String, Object> bogoOnlyResult;
    Map<String, Object> noPromoResult;

    @Given("no promotions are applied")
    public void noPromotionsAreApplied() {
        bogoCosmeticsActive = false;
        threshold = 0;
        discount = 0;
    }

    @Given("the threshold discount promotion is configured:")
    public void thresholdDiscountConfigured(DataTable table) {
        Map<String, String> config = table.asMaps(String.class, String.class).get(0);
        threshold = Integer.parseInt(config.get("threshold"));
        discount = Integer.parseInt(config.get("discount"));
    }

    @Given("the buy one get one promotion for cosmetics is active")
    public void bogoCosmeticsActive() {
        bogoCosmeticsActive = true;
    }

    @When("a customer places an order with:")
    public void customerPlacesOrder(DataTable table) {
        orderItems = table.asMaps(String.class, String.class);
        if (bogoCosmeticsActive && threshold > 0) {
            stackedResult = orderService.calculateStackedPromotions(orderItems, threshold, discount);
        } else if (bogoCosmeticsActive) {
            bogoOnlyResult = orderService.calculateBogoCosmetics(orderItems);
        } else if (threshold > 0) {
            // Compose result to match expected structure
            Map<String, Integer> summary = orderService.calculateWithThresholdDiscount(orderItems, threshold, discount);
            thresholdResult = new HashMap<>();
            thresholdResult.putAll(summary);
            List<Map<String, String>> received = new ArrayList<>();
            for (Map<String, String> item : orderItems) {
                Map<String, String> receivedItem = new HashMap<>();
                receivedItem.put("productName", item.get("productName"));
                receivedItem.put("quantity", item.get("quantity"));
                received.add(receivedItem);
            }
            thresholdResult.put("received", received);
        } else {
            int total = orderService.calculateTotalAmount(orderItems);
            noPromoResult = new HashMap<>();
            noPromoResult.put("totalAmount", total);
            List<Map<String, String>> received = new ArrayList<>();
            for (Map<String, String> item : orderItems) {
                Map<String, String> receivedItem = new HashMap<>();
                receivedItem.put("productName", item.get("productName"));
                receivedItem.put("quantity", item.get("quantity"));
                received.add(receivedItem);
            }
            noPromoResult.put("received", received);
        }
    }

    @Then("the order summary should be:")
    public void orderSummaryShouldBe(DataTable table) {
        Map<String, String> expected = table.asMaps(String.class, String.class).get(0);
        Map<String, Object> actual;
        if (stackedResult != null) {
            actual = stackedResult;
        } else if (bogoOnlyResult != null) {
            actual = bogoOnlyResult;
        } else if (thresholdResult != null) {
            actual = thresholdResult;
        } else {
            actual = noPromoResult;
        }
        for (String key : expected.keySet()) {
            Assertions.assertEquals(Integer.parseInt(expected.get(key)), ((Number)actual.get(key)).intValue(), "Mismatch for: " + key);
        }
    }

    @And("the customer should receive:")
    public void customerShouldReceive(DataTable table) {
        List<Map<String, String>> expected = table.asMaps(String.class, String.class);
        List<Map<String, String>> actual;
        if (stackedResult != null) {
            actual = (List<Map<String, String>>) stackedResult.get("received");
        } else if (bogoOnlyResult != null) {
            actual = (List<Map<String, String>>) bogoOnlyResult.get("received");
        } else if (thresholdResult != null) {
            actual = (List<Map<String, String>>) thresholdResult.get("received");
        } else {
            actual = (List<Map<String, String>>) noPromoResult.get("received");
        }
        Assertions.assertEquals(expected, actual);
    }
}
