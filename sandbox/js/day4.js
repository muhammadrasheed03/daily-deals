// import only what we need from utils.js
import { formatPrice, calcDiscountPercent, isGoodDeal, formatDeal} from './utils.js'

const deals = [
    {name: "Dell XPS 15", price: 899.99, original_price: 1199.99, retailer: "Dell"},
    {name: "Sony Headphones", price: 279.99, original_price: 399.99, retailer: "Sony"},
    {name: "USB Cable", price: 8.99, original_price: 9.99, retailer: "Amazon"},
]

//use our imported utiliites
deals.forEach(deal=> {
    console.log(formatDeal(deal))
    console.log(`Good deal? ${isGoodDeal(deal.price, deal.original_price)}`)
    console.log("---")
})