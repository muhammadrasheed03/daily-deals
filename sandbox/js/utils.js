//named exports - utility functions for dealing with deal data

export const formatPrice = (price) =>   `$${price.toFixed(2)}`

export const calcDiscountPercent = (price, originalPrice) =>
((1-price/originalPrice)*100).toFixed(1)

export const isGoodDeal = (price, original_price, threshold=20) =>
    calcDiscountPercent(price, original_price) >=threshold

export const formatDeal = ({name, price, original_price, retailer}) =>
    `${retailer} | ${name} | ${formatPrice(price)} | ${calcDiscountPercent(price, original_price)}% off`