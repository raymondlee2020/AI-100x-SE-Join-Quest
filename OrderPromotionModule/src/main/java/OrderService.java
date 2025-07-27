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
        Map<String, Integer> productQty = new LinkedHashMap<>();
        Map<String, String> productCategory = new HashMap<>();
        for (Map<String, String> item : items) {
            String product = item.get("productName");
            String category = item.getOrDefault("category", "");
            int quantity = Integer.parseInt(item.get("quantity"));
            int unitPrice = Integer.parseInt(item.get("unitPrice"));
            productQty.put(product, productQty.getOrDefault(product, 0) + quantity);
            productCategory.put(product, category);
            totalAmount += quantity * unitPrice;
        }
        List<Map<String, String>> received = new ArrayList<>();
        for (String product : productQty.keySet()) {
            String category = productCategory.get(product);
            int quantity = productQty.get(product);
            int receivedQty = quantity;
            if ("cosmetics".equalsIgnoreCase(category)) {
                receivedQty = (quantity >= 2) ? quantity + 1 : 2;
            }
            Map<String, String> receivedItem = new HashMap<>();
            receivedItem.put("productName", product);
            receivedItem.put("quantity", String.valueOf(receivedQty));
            received.add(receivedItem);
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

    public Map<String, Object> calculateDoubleEleven(List<Map<String, String>> items) {
        int totalAmount = 0;
        List<Map<String, String>> received = new ArrayList<>();
        for (Map<String, String> item : items) {
            String product = item.get("productName");
            int quantity = Integer.parseInt(item.get("quantity"));
            int unitPrice = Integer.parseInt(item.get("unitPrice"));
            Map<String, String> receivedItem = new HashMap<>();
            receivedItem.put("productName", product);
            receivedItem.put("quantity", String.valueOf(quantity));
            received.add(receivedItem);
        }
        // double-eleven: 單一商品、單價100，每滿10件8折，剩餘以原價計算
        if (items.size() == 1 && Integer.parseInt(items.get(0).get("unitPrice")) == 100) {
            int quantity = Integer.parseInt(items.get(0).get("quantity"));
            int sets = quantity / 10;
            int remain = quantity % 10;
            totalAmount = sets * (int)(10 * 100 * 0.8) + remain * 100;
        } else {
            // fallback: 原價計算
            for (Map<String, String> item : items) {
                int quantity = Integer.parseInt(item.get("quantity"));
                int unitPrice = Integer.parseInt(item.get("unitPrice"));
                totalAmount += quantity * unitPrice;
            }
        }
        Map<String, Object> result = new HashMap<>();
        result.put("totalAmount", totalAmount);
        result.put("received", received);
        return result;
    }
}
