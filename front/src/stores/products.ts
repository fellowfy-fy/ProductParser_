import { defineStore } from "pinia"
import { PaginatedProductList, Product, ProductService } from "src/client"
import { storeShortcut } from "src/modules/StoreCrud"

export const useProductsStore = defineStore("products", {
  state: () => ({
    product: null as Product | null,
    products: null as Product[] | null,
  }),

  getters: {},

  actions: {
    loadProducts(payload: object): Promise<PaginatedProductList> {
      return storeShortcut({
        promise: ProductService.productList(payload),
        setValue: (resp: PaginatedProductList) => {
          this.products = resp.results as []
        },
      })
    },
    loadProduct(id: number): Promise<Product> {
      return storeShortcut({
        promise: ProductService.productRetrieve({ id }),
        setValue: (resp: Product) => {
          this.product = resp
        },
      })
    },
    deleteProduct(id: number): Promise<Product> {
      return storeShortcut({
        promise: ProductService.productDestroy({ id }),
        setValue: (resp) => {
          this.product = null
        },
      })
    },
    createProduct(payload: Product): Promise<Product> {
      return storeShortcut({
        promise: ProductService.productCreate({ requestBody: payload }),
        setValue: (resp: Product) => {
          this.product = resp
        },
      })
    },
    updateProduct(id: number, payload: Product): Promise<Product> {
      return storeShortcut({
        promise: ProductService.productUpdate({ id, requestBody: payload }),
        setValue: (resp: Product) => {
          this.product = resp
        },
      })
    },
  },
})
