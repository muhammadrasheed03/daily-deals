// ---- var vs let vs const ----

// 1. hoisting with var
console.log("1. hoisting:")
console.log(productName)
var productName = "Dell XPS 15"
console.log(productName)

// 2. block scope with let
console.log("\n2. block scope:")
const deals = [
    {name: "Laptop", price: 899.99},
    {name: "Headphones", price: 279.99},
    {name: "USB Cable", price: 8.99}
]

for(let i= 0; i< deals.length; i++){
    let currentDeal = deals[i]
    console.log(`${currentDeal.name}: $${currentDeal.price}`)

}
// console.log(currentDeal) // would this work? try uncommenting it

// 3. const doesn't mean immutable
console.log("\n3. const with objects:")
const deal = {name: "Sony Headphones", price: 279.99}
deal.price = 259.99 //this works fine
console.log(deal.price) //why?
//deal = {name: "other"} // this would fail, why?

// ---- arrow functions, template literals, destructuring

//regular function vs arrow function
function getDiscount(price, originalPrice){
    return ((1-price/originalPrice)*100).toFixed(1)
}

const getDiscountArrow = (price, originalPrice) => {
    return ((1-price/originalPrice)*100).toFixed(1)
}

// single expression — implicit return, no braces needed
const getDiscountShort = (price, originalPrice) =>
    ((1 - price / originalPrice) * 100).toFixed(1)

console.log("\n4. arrow functions:")
console.log(getDiscount(899.99, 1199.99))
console.log(getDiscountArrow(899.99, 1199.99))
console.log(getDiscountShort(899.99, 1199.99))

//destructuring objects
console.log("\n5. object destructuring:")
const product = {name: "Dell XPS 15", price: 899.99, retailer: "Dell", inStock: true}

const{name, price, retailer} = product // pull out only what you need
console.log(`${name} from ${retailer}: $${price}`)

//destructuring with rename
const {price: currentPrice, name: productTitle } = product
console.log(`${productTitle} costs $${currentPrice}`)

//destructuring arrays
console.log("\n6. array destructuring:")
const prices = [899.99, 949.99, 879.99, 919.99]
const [first, second, ...rest] = prices
console.log(`First: $${first}, Second: $${second}, Rest: ${rest}`)

//destructuring in function params - very common in React
const formatDeal = ({name, price, retailer}) =>
    `${retailer} | ${name} | $${price}`

console.log(formatDeal(product))

// ---- closures ----
console.log("\n7.closures:")

const createPriceChecker = (threshold) => {
    return(price) => price <= threshold
}

const under500 = createPriceChecker(500)
const under100 = createPriceChecker(100)

console.log(under500(899.99)) //what prints?
console.log(under500(299.99)) //what prints?
console.log(under100(89.99)) //what prints?
console.log(under100(299.99)) //what prints?

// ---- event loop ----
console.log("\n8.event loop:")

console.log("1-start")

setTimeout(() => {
    console.log("2 - setTimeout")
}, 0)

Promise.resolve().then(() =>{
    console.log("3 - promise")
})

console.log("4 - end")