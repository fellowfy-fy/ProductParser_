import { defineStore } from "pinia"
import { Category, CategoryService, PaginatedCategoryList, PaginatedProductList, Product, ProductService, StatusOkCount } from "src/client"
import { storeShortcut } from "src/Modules/StoreCrud"

export const useProductsStore = defineStore("products", {
  state: () => ({
    product: null as Product | null,
    products: null as Product[] | null,
    category: null as Category | null,
    categories: null as Category[] | null,
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
        setValue: () => {
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
    // Categories
    loadCategories(payload: object): Promise<PaginatedCategoryList> {
      return storeShortcut({
        promise: CategoryService.categoryList(payload),
        setValue: (resp: PaginatedCategoryList) => {
          this.categories = resp.results as []
        },
      })
    },
    loadCategory(id: number): Promise<Category> {
      return storeShortcut({
        promise: CategoryService.categoryRetrieve({ id }),
        setValue: (resp: Category) => {
          this.category = resp
        },
      })
    },
    deleteCategory(id: number): Promise<Category> {
      return storeShortcut({
        promise: CategoryService.categoryDestroy({ id }),
        setValue: () => {
          this.category = null
        },
      })
    },
    createCategory(payload: Category): Promise<Category> {
      return storeShortcut({
        promise: CategoryService.categoryCreate({ formData: payload }),
        setValue: (resp: Category) => {
          this.category = resp
        },
      })
    },
    updateCategory(id: number, payload: Category): Promise<Category> {
      return storeShortcut({
        promise: CategoryService.categoryUpdate({ id, formData: payload }),
        setValue: (resp: Category) => {
          this.category = resp
        },
      })
    },

    //
    importProducts(file: Blob): Promise<StatusOkCount> {
      return storeShortcut({
        promise: ProductService.productImportProductsCreate({ formData: { file: file } }),
      })
    },
  },
})
