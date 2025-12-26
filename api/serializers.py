from rest_framework import serializers
from restaurant.models import Table, MenuItem
from orders.models import Order, OrderItem
from billing.models import Bill

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id","number","capacity","status"]

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id","name","category","price","is_available"]

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(source="menu_item", queryset=MenuItem.objects.all(), write_only=True)
    class Meta:
        model = OrderItem
        fields = ["id","menu_item","menu_item_id","quantity"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ["id","table","status","created_at","updated_at","items"]

    def create(self, validated_data):
        items = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)
        for it in items:
            OrderItem.objects.create(order=order, **it)
        return order

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ["id","table","order","status","subtotal","tax_amount","total","created_at","paid_at"]
