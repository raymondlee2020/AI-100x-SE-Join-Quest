package main.java;

import java.util.*;

public class OrderService {
    public int calculateTotalAmount(List<Map<String, String>> items) {
        int total = 0;
        for (Map<String, String> item : items) {
            int quantity = Integer.parseInt(item.get("quantity"));
            int unitPrice = Integer.parseInt(item.get("unitPrice"));
            total += quantity * unitPrice;
        }
        return total;
    }

    public Map<String, Integer> calculateWithThresholdDiscount(List<Map<String, String>> items, int threshold, int discount) {
        int originalAmount = 0;
        for (Map<String, String> item : items) {
            int quantity = Integer.parseInt(item.get("quantity"));
            int unitPrice = Integer.parseInt(item.get("unitPrice"));
            originalAmount += quantity * unitPrice;
        }
        int appliedDiscount = originalAmount >= threshold ? discount : 0;
        int totalAmount = originalAmount - appliedDiscount;
        Map<String, Integer> result = new HashMap<>();
        result.put("originalAmount", originalAmount);
        result.put("discount", appliedDiscount);
        result.put("totalAmount", totalAmount);
        return result;
    }

    public Map<String, Object> calculateBogoCosmetics(List<Map<String, String>> items) {
        int totalAmount = 0;
        List<Map<String, String>> received = new ArrayList<>();
        for (Map<String, String> item : items) {
            String category = item.getOrDefault("category", "");
            int quantity = Integer.parseInt(item.get("quantity"));
            int unitPrice = Integer.parseInt(item.get("unitPrice"));
            int receivedQty = quantity;
            if ("cosmetics".equalsIgnoreCase(category)) {
                receivedQty = quantity * 2;
            }
            Map<String, String> receivedItem = new HashMap<>();
            receivedItem.put("productName", item.get("productName"));
            receivedItem.put("quantity", String.valueOf(receivedQty));
            received.add(receivedItem);
            totalAmount += quantity * unitPrice;
        }
        Map<String, Object> result = new HashMap<>();
        result.put("totalAmount", totalAmount);
        result.put("received", received);
        return result;
    }

    public Map<String, Object> calculateStackedPromotions(List<Map<String, String>> items, int threshold, int discount) {
        int originalAmount = 0;
        List<Map<String, String>> received = new ArrayList<>();
        for (Map<String, String> item : items) {
            String category = item.getOrDefault("category", "");
            int quantity = Integer.parseInt(item.get("quantity"));
            int unitPrice = Integer.parseInt(item.get("unitPrice"));
            int receivedQty = quantity;
            if ("cosmetics".equalsIgnoreCase(category)) {
                receivedQty = quantity * 2;
            }
            Map<String, String> receivedItem = new HashMap<>();
            receivedItem.put("productName", item.get("productName"));
            receivedItem.put("quantity", String.valueOf(receivedQty));
            received.add(receivedItem);
            originalAmount += quantity * unitPrice;
        }
        int appliedDiscount = originalAmount >= threshold ? discount : 0;
        int totalAmount = originalAmount - appliedDiscount;
        Map<String, Object> result = new HashMap<>();
        result.put("originalAmount", originalAmount);
        result.put("discount", appliedDiscount);
        result.put("totalAmount", totalAmount);
        result.put("received", received);
        return result;
    }
}
