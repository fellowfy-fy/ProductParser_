<template>
  <q-select
    v-model="model"
    :loading="loading"
    :options="products"
    options-dense
    option-label="name"
    option-value="id"
    map-options
    emit-value
    outlined
    multiple
    use-chips
    v-bind="$attrs"
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
  }
  const prom = store.loadProducts(payload)
  promiseSetLoading(prom, loading)
}

onMounted(() => loadData())

</script>