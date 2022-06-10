<template>
  <div class="popup">
    <div class="popup-inner">
      <slot />

      <button class="popup-close">Filter</button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99;
  background-color: aquamarine;
  display: flex;
  align-items: center;
  justify-content: center;
}

.popup-inner {
  background-color: aquamarine;
  padding: 32px;
}
</style>

<script>
export default {};
</script>
