<template>
  <q-select
    v-model="model"
    :loading="loading"
    :options="categories"
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
import { promiseSetLoading } from 'src/Modules/StoreCrud';

const props = defineProps({
  modelValue: {
    type: Array as PropType<number[]>,
    required: true,
    default: undefined,
  },
})

const $emit = defineEmits(['update:model-value'])

const store = useProductsStore()
const {categories} = storeToRefs(store)

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
    pageSize: 1000
  }
  const prom = store.loadCategories(payload)
  promiseSetLoading(prom, loading)
}

onMounted(() => loadData())

</script>