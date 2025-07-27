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

    @Given("no promotions are applied")
    public void noPromotionsAreApplied() {
        // 無需特殊處理
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
        }
    }

    @Then("the order summary should be:")
    public void orderSummaryShouldBe(DataTable table) {
        Map<String, String> expected = table.asMaps(String.class, String.class).get(0);
        Assertions.assertEquals(Integer.parseInt(expected.get("originalAmount")), stackedResult.get("originalAmount"));
        Assertions.assertEquals(Integer.parseInt(expected.get("discount")), stackedResult.get("discount"));
        Assertions.assertEquals(Integer.parseInt(expected.get("totalAmount")), stackedResult.get("totalAmount"));
    }

    @And("the customer should receive:")
    public void customerShouldReceive(DataTable table) {
        List<Map<String, String>> expected = table.asMaps(String.class, String.class);
        List<Map<String, String>> actual = (List<Map<String, String>>) stackedResult.get("received");
        Assertions.assertEquals(expected, actual);
    }
}
