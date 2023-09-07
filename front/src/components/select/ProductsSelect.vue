<template>
  <q-select
    v-model="model"
    :loading="loading"
    :options="products"
    options-dense
    option-label="name"
    option-value="id"
    map-options
    outlined
    multiple
    use-chips
    use-input
    v-bind="$attrs"
    style="max-width: 100%"
    @filter="onFilter"
  />
</template>

<script setup lang="ts">
import { PropType, computed, onMounted, ref } from 'vue';
import { useProductsStore } from "src/stores/products"
import { storeToRefs } from 'pinia';
import { promiseSetLoading } from 'src/modules/StoreCrud';

const props = defineProps({
  modelValue: {
    type: Array as PropType<number[]>,
    required: true,
    default: undefined,
  },
})

const $emit = defineEmits(['update:model-value'])

const store = useProductsStore()
const {products} = storeToRefs(store)

const loading = ref(false)
const search = ref("")

const model = computed({
  get(){
    return props.modelValue
  },
  set(val){
    $emit('update:model-value', val)
  }
})

function loadData() {
  const payload = {
    search: search.value,
  }
  const prom = store.loadProducts(payload)
  promiseSetLoading(prom, loading)
  return prom;
}

function onFilter(value: string, update: CallableFunction){
  search.value = value
  update(() => {
    void loadData()
  })
}

onMounted(() => loadData())

</script>